

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b d)
(ontable c)
(on d h)
(ontable e)
(on f a)
(ontable g)
(on h i)
(on i e)
(clear b)
(clear c)
(clear f)
(clear g)
)
(:goal
(and
(on b g)
(on c d)
(on d f)
(on e i)
(on f b)
(on g e)
(on h c)
(on i a))
)
)


