

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a e)
(ontable b)
(on c h)
(on d g)
(on e f)
(on f c)
(ontable g)
(on h b)
(on i a)
(clear d)
(clear i)
)
(:goal
(and
(on a e)
(on c h)
(on e f)
(on f g)
(on h i)
(on i d))
)
)


