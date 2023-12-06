

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a c)
(on b d)
(on c g)
(on d f)
(ontable e)
(on f i)
(on g e)
(on h b)
(ontable i)
(clear a)
(clear h)
)
(:goal
(and
(on b d)
(on c i)
(on d g)
(on f b)
(on g a)
(on h c)
(on i e))
)
)


